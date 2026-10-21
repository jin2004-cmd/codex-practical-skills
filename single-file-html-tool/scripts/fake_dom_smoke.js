#!/usr/bin/env node
/**
 * fake_dom_smoke.js — 单文件 HTML 工具的「假 DOM」冒烟测试脚手架。
 *
 * 为什么需要它：
 *   node --check 只校验语法，抓不到「首屏就崩」这类运行时错误。
 *   单文件 HTML 里的 <script> 无法在 Node 里直接跑，因为没有 document / localStorage。
 *   本脚本 stub 掉这些，用 new Function 真正执行一遍页面代码，
 *   再把内部函数 export 出来做断言。
 *
 * 用法：
 *   node fake_dom_smoke.js <target.html>            # 只跑「能不能活着执行完」
 *   node fake_dom_smoke.js <target.html> --export DB,stats,render
 *                                                    # 额外把内部符号导出，供你写断言
 *
 * 退出码：0 = 通过；1 = 执行抛错（首屏崩溃）
 *
 * 定制断言：复制本文件到你的项目里，在 `// === 你的断言写在这里 ===` 处补充。
 */

'use strict';
const fs = require('fs');
const path = require('path');

// ---------- 参数 ----------
const argv = process.argv.slice(2);
const file = argv.find(a => !a.startsWith('--'));
const exportIdx = argv.indexOf('--export');
const exportList = exportIdx >= 0 && argv[exportIdx + 1]
  ? argv[exportIdx + 1].split(',').map(s => s.trim()).filter(Boolean)
  : [];

if (!file) {
  console.error('用法: node fake_dom_smoke.js <target.html> [--export DB,stats,render]');
  process.exit(2);
}
const target = path.resolve(file);
if (!fs.existsSync(target)) {
  console.error('文件不存在: ' + target);
  process.exit(2);
}

// ---------- 假 DOM ----------
const els = {};

function mkEl(id) {
  const cls = new Set();
  const el = {
    id: id || '',
    tagName: 'DIV',
    textContent: '', innerHTML: '', value: '',
    style: {}, dataset: {}, children: [], files: [],
    isCard: false, offsetWidth: 1, parentNode: null,
    focus() {}, click() {}, select() {}, remove() {},
    addEventListener() {}, appendChild() {}, removeChild() {},
    setAttribute() {}, getAttribute() { return null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    closest() { return null; },
    getBoundingClientRect() { return { left: 0, top: 0, width: 10, height: 10 }; }
  };
  el.classList = {
    add(...c) { c.forEach(x => cls.add(x)); },
    remove(...c) { c.forEach(x => cls.delete(x)); },
    toggle(c, f) {
      if (f === undefined) f = !cls.has(c);
      f ? cls.add(c) : cls.delete(c);
      return f;
    },
    contains(c) { return cls.has(c); },
    get size() { return cls.size; }
  };
  return el;
}

global.document = {
  getElementById(id) { return els[id] || (els[id] = mkEl(id)); },
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
  createElement() { return mkEl('tmp'); },
  body: { appendChild() {}, classList: mkEl('body').classList }
};

const store = {};
global.localStorage = {
  getItem(k) { return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null; },
  setItem(k, v) { store[k] = String(v); },
  removeItem(k) { delete store[k]; },
  clear() { Object.keys(store).forEach(k => delete store[k]); }
};

global.window = {
  addEventListener() {}, removeEventListener() {},
  location: { href: '', hash: '' },
  innerWidth: 1440, innerHeight: 900,
  matchMedia() { return { matches: false, addEventListener() {}, addListener() {} }; },
  requestAnimationFrame() { return 0; },
  cancelAnimationFrame() {},
  scrollTo() {}, open() { return null; }, print() {},
  localStorage: global.localStorage
};

// Node 22 起 globalThis.navigator 是只读 getter，必须用 defineProperty 覆盖
Object.defineProperty(global, 'navigator', {
  value: { userAgent: 'node', clipboard: { writeText() { return Promise.resolve(); } } },
  configurable: true, writable: true
});

global.confirm = () => true;
global.alert = () => {};
global.prompt = () => null;

// 🔴 千万不要整体覆盖 global.URL / global.Blob
// Node 22 内部 fs shim 会用到 URL（filePath instanceof URL），
// 一旦被替换成普通对象，所有 readFileSync 立刻抛
// "Right-hand side of 'instanceof' is not callable"
// 只在缺失时补齐，已存在的原生实现一律保留
if (typeof global.Blob === 'undefined') {
  global.Blob = class { constructor(parts) { this.parts = parts; } };
}
if (typeof global.URL === 'undefined') { global.URL = {}; }
if (typeof global.URL.createObjectURL !== 'function') {
  global.URL.createObjectURL = () => 'blob:x';
}
if (typeof global.URL.revokeObjectURL !== 'function') {
  global.URL.revokeObjectURL = () => {};
}
global.FileReader = class {
  readAsText(f) { this.onload({ target: { result: f.__text } }); }
};

// 让「数字滚动动画」同步跑完，方便读最终值
let fakeNow = 0;
const realDateNow = Date.now;
Date.now = () => fakeNow;
global.setTimeout = (fn) => { fakeNow += 600; try { fn(); } catch (e) { /* 交给外层 */ } return 0; };
global.clearTimeout = () => {};
global.setInterval = () => 0;
global.clearInterval = () => {};

// ---------- 执行页面代码 ----------
const html = fs.readFileSync(target, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) {
  console.error('没找到 <script> 块');
  process.exit(2);
}
const code = m[1];

let api;
try {
  api = new Function(code + '\n;return {' + exportList.join(',') + '};')();
} catch (e) {
  console.error('\n❌ 页面脚本执行抛错（首屏崩溃）:');
  console.error('   ' + e.message);
  console.error('   ' + (e.stack || '').split('\n')[1]);
  process.exit(1);
}

console.log('✅ 页面脚本执行完成，无运行时异常');
console.log('   文件: %s (%d KB)', path.basename(target),
  Math.round(fs.statSync(target).size / 1024));

if (exportList.length) {
  const missing = exportList.filter(k => !(k in api));
  if (missing.length) {
    console.error('❌ 以下符号导出失败: ' + missing.join(', '));
    process.exit(1);
  }
  console.log('✅ 导出符号齐全: ' + exportList.join(', '));
}

// === 你的断言写在这里 ===
// 参考：
// const s = api.stats();
// assert(s.total === 556, 'total 应为 556，实际 ' + s.total);

function assert(cond, msg) {
  if (!cond) { console.error('❌ ' + msg); process.exitCode = 1; }
  else { console.log('   PASS  ' + msg); }
}

module.exports = { assert, api, els, store, html };
