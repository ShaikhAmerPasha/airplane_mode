frappe.ready(async function() {
  // Ensure Flight Price is always read-only
  frappe.web_form.fields_dict.flight_price.df.read_only = 1;
  frappe.web_form.refresh_field('flight_price');

  // Grab query params from URL (e.g. ?flight=FLT-0001&price=5000)
  const q = frappe.utils.get_query_params();

  if (q.flight) {
    // Set the Flight field
    await frappe.web_form.set_value('flight', q.flight);

    // Prefer price passed in URL, otherwise fetch from Flight doctype
    if (q.price) {
      await frappe.web_form.set_value('flight_price', q.price);
    } else {
      const r = await frappe.db.get_value('Airplane Flight', q.flight, 'ticket_price');
      if (r && r.message) {
        await frappe.web_form.set_value('flight_price', r.message.ticket_price);
      }
    }
  }
});
