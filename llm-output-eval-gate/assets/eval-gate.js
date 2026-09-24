/* eval-gate.js — two-layer quality gate for LLM outputs.
 * Vanilla JS, zero dependencies. Works in browser (window.EvalGate) and Node (module.exports).
 *
 * Usage:
 *   var res = await EvalGate.gate({
 *     name: "plan",
 *     generate: async function (attempt) { ... return parsed LLM result ... },
 *     validate: function (result) { return { pass: true|false, issues: [...] }; },
 *     judge:    async function (result) { return { score: 0-10, comment: "" }; },
 *     threshold: 7,      // optional, default 7
 *     maxRetries: 2      // optional, default 2
 *   });
 *   // res = { ok, result, report }
 *   // report = { name, attempts:[{attempt,pass,issues,score,comment}], retries, finalPass, finalScore, threshold }
 */
(function (root, factory) {
  var lib = factory();
  if (typeof module === "object" && module.exports) module.exports = lib;
  else root.EvalGate = lib;
})(typeof self !== "undefined" ? self : this, function () {

  /**
   * Quality gate main flow: generate → L1 validate → L2 judge → retry if below threshold.
   * Falls back to the best attempt when nothing passes; never returns unvalidated output silently.
   */
  async function gate(opts) {
    var threshold = opts.threshold == null ? 7 : opts.threshold;
    var maxRetries = opts.maxRetries == null ? 2 : opts.maxRetries;
    var attempts = [];
    var best = null;

    for (var attempt = 0; attempt <= maxRetries; attempt++) {
      var result = await opts.generate(attempt);
      var v = opts.validate(result);
      var j = v.pass
        ? await opts.judge(result)
        : { score: 0, comment: "rule validation failed, scoring skipped" };
      var rec = {
        attempt: attempt + 1,
        pass: v.pass && j.score >= threshold,
        issues: v.issues || [],
        score: j.score,
        comment: j.comment
      };
      attempts.push(rec);

      if (!best || (v.pass && j.score > (best._score || -1))) {
        best = result;
        best._score = v.pass ? j.score : -1;
      }
      if (rec.pass) break;
    }

    var finalRec = attempts[attempts.length - 1];
    var report = {
      name: opts.name,
      attempts: attempts,
      retries: attempts.length - 1,
      finalPass: finalRec.pass,
      finalScore: finalRec.score,
      threshold: threshold
    };

    if (best && best._score !== undefined) delete best._score;
    return { ok: finalRec.pass, result: finalRec.pass ? result : best, report: report };
  }

  /* ---------- Example L1: task-plan constraints (adapt per domain) ---------- */
  function validatePlanExample(tasks, maxMinutes) {
    var issues = [];
    if (!Array.isArray(tasks)) return { pass: false, issues: ["output is not a task array"] };
    if (tasks.length < 3) issues.push("too few tasks (" + tasks.length + " < 3)");
    if (tasks.length > 5) issues.push("too many tasks (" + tasks.length + " > 5)");
    var total = 0, seen = {};
    tasks.forEach(function (t, i) {
      var tag = "task " + (i + 1);
      if (!t || typeof t !== "object") { issues.push(tag + ": not an object"); return; }
      if (!t.title || !String(t.title).trim()) issues.push(tag + ": missing title");
      if (["high", "mid", "low"].indexOf(t.priority) < 0) issues.push(tag + ": illegal priority");
      var m = parseInt(t.minutes, 10);
      if (!m || m < 5 || m > 240) issues.push(tag + ": minutes out of range (5-240)");
      else total += m;
      if (t.title) {
        var k = String(t.title).trim();
        if (seen[k]) issues.push(tag + ": duplicate title");
        seen[k] = true;
      }
    });
    if (maxMinutes && total > maxMinutes) {
      issues.push("total " + total + "min exceeds budget " + maxMinutes + "min");
    }
    return { pass: issues.length === 0, issues: issues, totalMinutes: total };
  }

  /* ---------- Example L2: heuristic scorer (offline fallback for LLM-as-Judge) ---------- */
  function heuristicScoreExample(tasks, maxMinutes) {
    if (!Array.isArray(tasks) || !tasks.length) return { score: 0, comment: "no valid tasks" };
    var score = 10, notes = [];
    var total = tasks.reduce(function (s, t) { return s + (parseInt(t.minutes, 10) || 0); }, 0);
    if (maxMinutes) {
      var util = total / maxMinutes;
      if (util < 0.4) { score -= 2; notes.push("time utilization low (" + Math.round(util * 100) + "%)"); }
      else if (util > 1) { score -= 4; notes.push("over time budget"); }
    }
    var high = tasks.filter(function (t) { return t.priority === "high"; }).length;
    if (high === 0) { score -= 2; notes.push("no high-priority task"); }
    else if (high > 2) { score -= 1; notes.push("too many high-priority tasks"); }
    score = Math.max(1, Math.min(10, score));
    return { score: score, comment: notes.join("; ") || "looks fine" };
  }

  return { gate: gate, validatePlanExample: validatePlanExample, heuristicScoreExample: heuristicScoreExample };
});
