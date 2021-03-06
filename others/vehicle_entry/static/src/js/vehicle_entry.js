odoo.define('vehicle_entry.vehicle_entry_enter', function (require) {
    var core = require('web.core');
    // var Model = require('web.Model');
    var Widget = require('web.Widget');
    var _t = core._t;
    var QWeb = core.qweb;
    // var _t = instance.web._t;
    var VehicleRecord = Widget.extend({
	events: {
	    template: "VehicleEntryTemplate",
	    "click .o_vehicle_entry_sign_in_out_icon": function() {
		this.$('.o_vehicle_entry_sign_in_out_icon').attr("disabled", "disabled");
		this.on_click();
	    },
	},

	start: function () {
            var self = this;

	    self.$el.html(QWeb.render("VechicleEntryTemplate", {widget: self}));

	    return this._super.apply(this, arguments);
	    
	},
	// template: "VehicleEntryTemplate",
	on_click: function() {
	    var self = this
	// new Model("vehicle_entry.vehicle_entry").call("auto_date_check_in"); 
        var action = ({
            type: 'ir.actions.act_window',
            res_model: 'vehicle_entry.vehicle_entry',
            view_type: 'form',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'current',
        })
        self.do_action(action)	    
	},  
	});
    
    core.action_registry.add('vehicle_entry_enter', VehicleRecord);

    return VehicleRecord;
});
