// Compare the real browser transformation with independent Python plot output.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const {makeItem, normalize} = require('../docs/static/ashby.js');
const fixture = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function canonical(item) {
  const refs = new Map(item.doc.roots.references.map(ref => [ref.id, ref]));
  const names = new Map();
  const models = [];
  function visit(value) {
    if (Array.isArray(value)) return value.map(visit);
    if (value && typeof value === 'object') {
      if (Object.keys(value).length === 1 && refs.has(value.id)) {
        if (!names.has(value.id)) {
          const n = models.length;
          names.set(value.id, n);
          models.push(null);
          const ref = refs.get(value.id);
          models[n] = {type: ref.type, attributes: visit(ref.attributes)};
        }
        return {ref: names.get(value.id)};
      }
      return Object.fromEntries(Object.keys(value).sort().map(key => [key, visit(value[key])]));
    }
    return value;
  }
  visit({id: item.root_id});
  return models;
}

assert.deepEqual(normalize(fixture.payload, [null, 'not a field', '']), fixture.payload.defaults);
const original = JSON.stringify(fixture.payload);
for (const test of fixture.cases) {
  const actual = canonical(makeItem(fixture.payload, test.fields));
  const expected = canonical(test.expected);
  function difference(a, b, path) {
    if (JSON.stringify(a) === JSON.stringify(b)) return null;
    if (a && b && typeof a === 'object' && typeof b === 'object') {
      for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) {
        const diff = difference(a[key], b[key], `${path}.${key}`);
        if (diff) return diff;
      }
    }
    return `${path}: ${JSON.stringify(a)?.slice(0, 200)} != ${JSON.stringify(b)?.slice(0, 200)}`;
  }
  const diff = difference(actual, expected, 'models');
  if (diff) throw new Error(`Plot parity ${test.fields.join(' / ')}: ${diff}`);
}
assert.equal(JSON.stringify(fixture.payload), original, 'Template mutation');
console.log(`${fixture.cases.length} JavaScript plot selections match original Python Bokeh documents.`);
