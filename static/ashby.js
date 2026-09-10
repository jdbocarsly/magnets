/* Bokeh 2.4.3 documents created by the original Python main_plot function.
 * Re-embedding resets zoom and tool state just like the original Flask reload.
 * The pure document transformation is also exercised by the parity checks.
 */
(function (global) {
  'use strict';

  function normalize(payload, values) {
    return values.map((value, i) => payload.fields.includes(value) ? value : payload.defaults[i]);
  }

  function makeItem(payload, values) {
    const selected = normalize(payload, values);
    const key = selected.map(field => payload.categories[field] ? 'c' : 'n').join('');
    const template = payload.templates[key];
    const item = JSON.parse(JSON.stringify(template.item));
    const refs = new Map(item.doc.roots.references.map(ref => [ref.id, ref]));
    template.axes.forEach((id, i) => { refs.get(id).attributes.axis_label = selected[i]; });
    template.glyphs.forEach(id => {
      const attrs = refs.get(id).attributes;
      attrs.x = {field: selected[0]};
      attrs.y = {field: selected[1]};
      if (key[2] === 'n') {
        for (const property of ['fill_color', 'line_color']) {
          if (attrs[property] && attrs[property].field !== undefined) {
            attrs[property].field = selected[2];
          }
        }
      }
    });
    template.mappers.forEach(id => {
      const attrs = refs.get(id).attributes;
      [attrs.low, attrs.high] = payload.stats[selected[2]];
    });
    return item;
  }

  // CommonJS supports document equivalence tests without requiring a browser.
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {makeItem, normalize};
    return;
  }

  async function start() {
    const payload = JSON.parse(document.getElementById('ashby-data').textContent);
    const controls = ['xaxis', 'yaxis', 'coloraxis'].map(id => document.getElementById(id));
    const names = ['x_axis', 'y_axis', 'color_axis'];
    const swap = document.getElementById('switch');
    let active = null;
    let queue = Promise.resolve();
    let generation = 0;

    function fromURL() {
      const params = new URLSearchParams(location.search);
      return normalize(payload, names.map(name => params.get(name)));
    }

    function query(values) {
      return new URLSearchParams(Object.fromEntries(names.map((name, i) => [name, values[i]])));
    }

    function update(values, push) {
      const selected = normalize(payload, values);
      controls.forEach((control, i) => { control.value = selected[i]; });
      const swapped = [selected[1], selected[0], selected[2]];
      swap.href = '?' + query(swapped);
      if (push) history.pushState(null, '', '?' + query(selected));
      const ticket = ++generation;
      queue = queue.then(async () => {
        if (ticket !== generation) return;
        if (!global.Bokeh) throw new Error('The Bokeh plotting library could not be loaded.');
        if (active) {
          const view = Bokeh.index[active];
          if (view) {
            const doc = view.model.document;
            if (doc) {
              // RootRemovedEvent removes the view and its Bokeh.index entry.
              doc.clear();
              const index = Bokeh.documents.indexOf(doc);
              if (index >= 0) Bokeh.documents.splice(index, 1);
            } else view.remove();
          }
        }
        document.getElementById('ashby-plot').replaceChildren();
        const item = makeItem(payload, selected);
        await Bokeh.embed.embed_item(item);
        active = item.root_id;
      }).catch(error => {
        console.error(error);
        document.getElementById('ashby-plot').textContent =
          'Unable to display the plot. Please reload the page and check your connection.';
      });
      return queue;
    }

    controls.forEach(control => control.addEventListener('change', () =>
      update(controls.map(input => input.value), true)));
    controls[0].form.addEventListener('submit', event => {
      event.preventDefault();
      update(controls.map(input => input.value), true);
    });
    swap.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      update([controls[1].value, controls[0].value, controls[2].value], true);
    });
    addEventListener('popstate', () => update(fromURL(), false));
    await update(fromURL(), false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})(typeof window === 'undefined' ? globalThis : window);
