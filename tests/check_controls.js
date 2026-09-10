// Exercise the actual DOM event handlers with a minimal DOM/Bokeh adapter.
// This checks lifecycle and history; it is not a substitute for visual QA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(new URL('../index.html', `file://${__filename}`), 'utf8');
const payload = JSON.parse(html.match(/id="ashby-data">(.*?)<\/script>/s)[1]);
const listeners = {};
const nodes = {};
function node(id) {
  return nodes[id] = {value: '', textContent: '', events: {},
    addEventListener(event, callback) { this.events[event] = callback; },
    replaceChildren() { this.textContent = ''; }};
}
for (const id of ['xaxis', 'yaxis', 'coloraxis', 'switch', 'ashby-plot', 'ashby-data']) node(id);
nodes['ashby-data'].textContent = JSON.stringify(payload);
nodes.xaxis.form = node('form');
const location = new URL('https://example.test/magnets/?x_axis=class&color_axis=class');
const visits = [];
const Bokeh = {index: {}, documents: [], embed: {
  async embed_item(item) {
    visits.push(item);
    const doc = {clear() { delete Bokeh.index[item.root_id]; }};
    Bokeh.documents.push(doc);
    Bokeh.index[item.root_id] = {model: {document: doc}};
  }}};
const context = {Bokeh, console, URLSearchParams, location,
  history: {pushState(_state, _unused, url) { location.href = new URL(url, location).href; }},
  addEventListener(event, callback) { listeners[event] = callback; },
  document: {readyState: 'loading', getElementById: id => nodes[id],
    addEventListener(event, callback) { listeners[event] = callback; }}};
context.window = context;
vm.runInNewContext(fs.readFileSync(new URL('../static/ashby.js', `file://${__filename}`), 'utf8'), context);
const flush = () => new Promise(resolve => setImmediate(resolve));
function axes() {
  return visits.at(-1).doc.roots.references.filter(ref => ref.type.endsWith('Axis'))
    .map(ref => ref.attributes.axis_label).sort();
}
(async () => {
  await listeners.DOMContentLoaded();
  assert.equal(nodes.xaxis.value, 'class');
  assert.equal(nodes.coloraxis.value, 'class');
  assert.equal(nodes.yaxis.value, payload.defaults[1]);
  nodes.xaxis.value = 'magnetic deformation (Σm), %';
  nodes.xaxis.events.change();
  await flush();
  assert.equal(location.searchParams.get('x_axis'), nodes.xaxis.value);
  assert(axes().includes(nodes.xaxis.value));
  const beforeSwap = [nodes.xaxis.value, nodes.yaxis.value];
  nodes.switch.events.click({button: 0, preventDefault() {}});
  await flush();
  assert.equal(nodes.xaxis.value, beforeSwap[1]);
  assert.equal(nodes.yaxis.value, beforeSwap[0]);
  location.search = '?x_axis=class&y_axis=class&color_axis=bad';
  listeners.popstate();
  await flush();
  assert.equal(nodes.xaxis.value, 'class');
  assert.equal(nodes.yaxis.value, 'class');
  assert.equal(nodes.coloraxis.value, payload.defaults[2]);
  for (const field of payload.fields) {
    nodes.coloraxis.value = field;
    nodes.coloraxis.events.change();
  }
  await flush();
  assert.equal(Bokeh.documents.length, 1, 'Old documents must be disposed');
  assert.equal(Object.keys(Bokeh.index).length, 1, 'Old views must be disposed');
  assert.equal(nodes['ashby-plot'].textContent, '');
  console.log('Ashby URL defaults, changes, swapping, history, rapid changes and disposal passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
