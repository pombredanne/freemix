/*global jQuery */
 (function($, Freemix) {

     // Display the view's UI.
     function display() {
         var content = this.getContent();
         root = Freemix.getTemplate("piechart-view-template");
         content.empty();
         root.appendTo(content);
         this.findWidget().recordPager();
     }

    function generateExhibitHTML() {
        var view = $("<div ex:role='view' ex:viewClass='Piechart' ex:viewLabel='" + this.config.name + "'></div>");
        var properties = [];
        var props = Freemix.property.enabledProperties();
        var config = this.config;
        $.each(config.metadata,
        function(index, metadata) {
            var property = metadata.property;
            var identify = props[property];
            if (!metadata.hidden && identify) {
                properties[properties.length] = property;
            }

        });
        view.attr("ex:groupProperties", properties.join(', '));
        return view;
    }

    Freemix.view.addViewType({
        label: "Pie Chart",
        thumbnail: "/static/exhibit/img/piechart-icon.png",
        display: display,
        generateExhibitHTML: generateExhibitHTML,
        config: {
            type: "piechart",
            metadata: []
        }
    });

})(window.Freemix.jQuery, window.Freemix);
