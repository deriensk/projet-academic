odoo.define('vehicle_entry.vehicle_entry_exit', function (require) {
    var core = require('web.core');
    // var Model = require('web.Model');
    var rpc = require('web.rpc');
    var Widget = require('web.Widget');
    var _t = core._t;
    var QWeb = core.qweb;
    // var _t = instance.web._t;
    var VehicleExit = Widget.extend({
	events: {
	    template: "VehicleExitTemplate",
	    "click .o_vehicle_entry_sign_in_out_icon": function() {
		this.$('.o_vehicle_entry_sign_in_out_icon').attr("disabled", "disabled");
		this.on_click();
	    },
    },
    
    start: function () {
        var self = this;

    self.$el.html(QWeb.render("VechicleExitTemplate", {widget: self}));

    return this._super.apply(this, arguments);
    
},


	// start: function () {
    //         var self = this;
    //         rpc.query({
    //             model: 'vehicle_entry.vehicle_entry',
    //            method: '_auto_date_time_out',
    //            args: ['']
    //         }).then(() => {
    //             console.log("hello miss")
    //         })
    //     },
	
	// template: "VehicleEntryTemplate",
	on_click: function() {   
        var self = this
        var action = ({
            type: 'ir.actions.act_window',
            name: 'vehicle_entry_tree_view_js',
            res_model: 'vehicle_entry.vehicle_entry',
            view_type: 'form',
            view_mode: 'list,form',
            views: [[false, 'list'], [false, 'form']],
            target: 'current',
	        // onclick: 'concept_out1()'
        }) 
        self.do_action(action)
    },  

    });


    
    core.action_registry.add('vehicle_entry_exit', VehicleExit);

    return VehicleExit;
});
