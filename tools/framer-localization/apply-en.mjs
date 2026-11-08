// Applique les traductions EN du copy deck dans la localisation Framer d'eagr.ai,
// via l'API serveur officielle de Framer (package `framer-api`).
//
//   FRAMER_API_KEY=... node apply-en.mjs              → simulation, rien n'est écrit
//   FRAMER_API_KEY=... node apply-en.mjs --apply      → écrit les traductions EN
//   FRAMER_API_KEY=... node apply-en.mjs --apply --publish
//                                                     → écrit, ajoute les redirections, publie
//
// Un rapport est écrit dans report.json et report.md à chaque exécution.

import { readFileSync, writeFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const HERE = dirname(fileURLToPath(import.meta.url))
const PROJECT_URL = process.env.FRAMER_PROJECT_URL ?? "https://framer.com/projects/eagr--Odh1KzTETxszYKEPZ2Zo"
const APPLY = process.argv.includes("--apply")
const PUBLISH = process.argv.includes("--publish")
const LOCALE_CODE = "en"

const data = JSON.parse(readFileSync(join(HERE, "translations.json"), "utf8"))

// ---------- normalisation et correspondance ----------

export function norm(s) {
    return String(s ?? "")
        .replace(/<[^>]+>/g, " ")
        .replace(/&nbsp;/g, " ")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;|&#34;/g, '"')
        .replace(/&#39;|&apos;/g, "'")
        .replace(/[   ]/g, " ")
        .replace(/[’‘]/g, "'")
        .replace(/[“”«»]/g, '"')
        .replace(/\s+/g, " ")
        .trim()
}

const key = (s) => norm(s).toLowerCase()

export function buildIndex(pairs) {
    const exact = new Map() // key -> [{en, scope}]
    const patterns = [] // {prefix, suffix, en, scope}
    for (const p of pairs) {
        if (p.kind === "pattern") {
            const [pre, suf = ""] = p.fr.split("[…]")
            const prefix = key(pre)
            const suffix = key(suf)
            if (prefix.length + suffix.length >= 15) patterns.push({ prefix, suffix, en: p.en, scope: p.scope })
            continue
        }
        const k = key(p.fr)
        if (!exact.has(k)) exact.set(k, [])
        exact.get(k).push({ en: p.en, scope: p.scope })
    }
    return { exact, patterns }
}

function groupMatchesScope(group, scope) {
    if (!scope) return false
    const name = String(group.name ?? "").toLowerCase()
    const s = scope.toLowerCase()
    if (s === "/") return name === "/" || name === "home" || name === "accueil"
    return name === s || name === s.slice(1) || name.endsWith(s)
}

export function lookup(index, sourceValue, group) {
    const k = key(sourceValue)
    if (!k) return null
    const candidates = index.exact.get(k) ?? index.patterns.filter((p) => k.startsWith(p.prefix) && k.endsWith(p.suffix))
    if (!candidates.length) return null
    const distinct = [...new Set(candidates.map((c) => c.en))]
    if (distinct.length === 1) return { en: distinct[0] }
    const scoped = candidates.filter((c) => groupMatchesScope(group, c.scope))
    const scopedDistinct = [...new Set(scoped.map((c) => c.en))]
    if (scopedDistinct.length === 1) return { en: scopedDistinct[0] }
    // "During the call" vs "During the call." : on garde la plus courte, c'est la même chaîne
    const stripped = [...new Set(distinct.map((e) => e.replace(/[.\s]+$/, "")))]
    if (stripped.length === 1) return { en: stripped[0] }
    return { ambiguous: distinct }
}

const escapeHtml = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")

// Pour un texte riche (HTML), on garde la balise du premier bloc et on remplace le contenu.
export function toFormatted(html, en) {
    const textSegments = String(html).replace(/<[^>]+>/g, "\u0000").split("\u0000").filter((t) => t.trim())
    const open = String(html).match(/^\s*<([a-z0-9]+)([^>]*)>/i)
    if (!open) return { value: escapeHtml(en), needsReview: textSegments.length > 1 }
    if (textSegments.length === 1) {
        const seg = textSegments[0]
        return { value: String(html).replace(seg, escapeHtml(en)), needsReview: false }
    }
    return { value: `<${open[1]}${open[2]}>${escapeHtml(en)}</${open[1]}>`, needsReview: true }
}

export function plan(groups, localeId, index, slugs) {
    const updates = {}
    const report = { set: [], unchanged: [], ambiguous: [], unmatchedFrench: [], skippedReadonly: [], slugs: [] }
    const looksFrench = (s) => /[àâçéèêëîïôûùüÿœ]|\b(le|la|les|des|vos|votre|nous|pour|avec|sans|chaque|appel|commercial)\b/i.test(s)
    for (const group of groups) {
        for (const source of group.sources) {
            const current = source.valueByLocale?.[localeId]
            if (current?.readonly) {
                report.skippedReadonly.push({ group: group.name, fr: source.value })
                continue
            }
            if (source.type === "slug") {
                const parts = String(source.value).split("/")
                const mapped = parts.map((p) => slugs[p] ?? p).join("/")
                if (mapped !== source.value) {
                    updates[source.id] = { [localeId]: { action: "set", value: mapped } }
                    report.slugs.push({ group: group.name, fr: source.value, en: mapped, before: current?.value ?? null })
                }
                continue
            }
            if (source.type === "link") continue
            const hit = lookup(index, source.value, group)
            if (!hit) {
                if (looksFrench(norm(source.value)) && (current?.value == null)) {
                    report.unmatchedFrench.push({ group: group.name, type: source.type, fr: norm(source.value).slice(0, 200) })
                }
                continue
            }
            if (hit.ambiguous) {
                report.ambiguous.push({ group: group.name, fr: norm(source.value), options: hit.ambiguous })
                continue
            }
            let value = hit.en
            let needsReview = false
            if (source.type === "formattedText") ({ value, needsReview } = toFormatted(source.value, hit.en))
            if (norm(current?.value) === norm(value)) {
                report.unchanged.push({ group: group.name, fr: norm(source.value) })
                continue
            }
            updates[source.id] = { [localeId]: { action: "set", value, ...(needsReview ? { needsReview: true } : {}) } }
            report.set.push({ group: group.name, type: source.type, fr: norm(source.value).slice(0, 160), en: norm(value).slice(0, 160), before: current?.value ? norm(current.value).slice(0, 160) : null, needsReview })
        }
    }
    return { updates, report }
}

function writeReport(report, extra) {
    writeFileSync(join(HERE, "report.json"), JSON.stringify({ ...extra, ...report }, null, 2))
    const lines = [
        `# Rapport localisation EN (${new Date().toISOString()})`,
        "",
        `Mode : ${extra.mode}`,
        "",
        `- Traductions écrites ou à écrire : ${report.set.length}`,
        `- Déjà correctes : ${report.unchanged.length}`,
        `- Slugs : ${report.slugs.length}`,
        `- Ambiguës (non écrites) : ${report.ambiguous.length}`,
        `- Textes FR sans traduction dans le deck : ${report.unmatchedFrench.length}`,
        `- Valeurs en lecture seule ignorées : ${report.skippedReadonly.length}`,
        "",
        "## Slugs",
        ...report.slugs.map((s) => `- ${s.fr} → ${s.en}`),
        "",
        "## Ambiguës",
        ...report.ambiguous.map((a) => `- [${a.group}] « ${a.fr} » : ${a.options.join(" | ")}`),
        "",
        "## Textes FR sans traduction",
        ...report.unmatchedFrench.map((u) => `- [${u.group}] (${u.type}) ${u.fr}`),
        "",
    ]
    writeFileSync(join(HERE, "report.md"), lines.join("\n"))
}

async function main() {
    if (!process.env.FRAMER_API_KEY) throw new Error("FRAMER_API_KEY manquante (Framer → Settings → API Keys).")
    const { connect } = await import("framer-api")
    const framer = await connect(PROJECT_URL, process.env.FRAMER_API_KEY)
    try {
        const locales = await framer.getLocales()
        const en = locales.find((l) => l.code === LOCALE_CODE || l.slug === LOCALE_CODE)
        if (!en) throw new Error(`Locale ${LOCALE_CODE} introuvable : ${locales.map((l) => l.code).join(", ")}`)
        const groups = await framer.getLocalizationGroups()
        const index = buildIndex(data.pairs)
        const { updates, report } = plan(groups, en.id, index, data.slugs)
        const mode = APPLY ? (PUBLISH ? "écriture + publication" : "écriture") : "simulation"
        const extra = { mode, project: PROJECT_URL, locale: en, groups: groups.length }

        if (APPLY && Object.keys(updates).length) {
            const ids = Object.keys(updates)
            const errors = []
            for (let i = 0; i < ids.length; i += 200) {
                const chunk = Object.fromEntries(ids.slice(i, i + 200).map((id) => [id, updates[id]]))
                const res = await framer.setLocalizationData({ valuesBySource: chunk })
                errors.push(...(res?.valuesBySource?.errors ?? []))
            }
            extra.writeErrors = errors

            if (report.slugs.length) {
                const existing = await framer.getRedirects()
                const have = new Set(existing.map((r) => r.from))
                const toAdd = report.slugs
                    .map((s) => ({ from: `/${LOCALE_CODE}/${String(s.fr).replace(/^\//, "")}`, to: `/${LOCALE_CODE}/${String(s.en).replace(/^\//, "")}`, expandToAllLocales: false }))
                    .filter((r) => r.from !== r.to && !have.has(r.from))
                if (toAdd.length) extra.redirectsAdded = (await framer.addRedirects(toAdd)).map((r) => `${r.from} → ${r.to}`)
            }

            if (PUBLISH) {
                const result = await framer.publish()
                extra.publish = { deployment: result.deployment?.id, hostnames: result.hostnames?.map((h) => h.hostname ?? h) }
                const hosts = JSON.stringify(extra.publish.hostnames ?? [])
                if (!hosts.includes("eagr.ai")) extra.deployedTo = await framer.deploy(result.deployment.id)
            }
        }
        writeReport(report, extra)
        console.log(JSON.stringify({ mode, set: report.set.length, unchanged: report.unchanged.length, slugs: report.slugs.length, ambiguous: report.ambiguous.length, unmatchedFrench: report.unmatchedFrench.length, writeErrors: extra.writeErrors?.length ?? 0, redirects: extra.redirectsAdded, publish: extra.publish }, null, 2))
    } finally {
        await framer.disconnect()
    }
}

if (import.meta.url === `file://${process.argv[1]}`) {
    main().catch((e) => {
        console.error(e)
        process.exit(1)
    })
}
