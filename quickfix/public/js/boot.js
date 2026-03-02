frappe.ready(function () {
	let shop_name = frappe.custom_job_card.quickfix_sname;

	if (shop_name) {
		$(".navbar-brand").append(
			`<span style="margin-left:10px; font-size:13px;">
                ${shop_name}
            </span>`
		);
	}
});
