MediaBrowser = {
    Grid: function() {
        return {
            'init': function() {
                // Insert image into CKEditor when image is clicked:
                var self = this;
                $(".use-image").click(function(evt) {
                    evt.preventDefault();
                    $.get($(this).attr("href"), {}, self.insert_image_callback);
                });
                // Add tool tips to images:
                $(".image-detail").each(function() {
                    var img = $(this);
                    img.qtip({
                        content: img.find("dl").html(),
                        show: 'mouseover',
                        hide: 'mouseout',
                    });
                });            
            },
            'insert_image_callback': function(data, status) {
                window.parent.MediaBrowser.Editor.add_image(data);
            }
        }
    }(),
    Template: function() {
        return {
            'init': function(full_size_img_src) {
                 this.url = full_size_img_src;
                 callback = this.insert_templated_image_callback;
                var self = this;
                $("form#template").submit(function (evt) { self.submit.apply(self, [evt])});
            },
            'submit': function(evt) {
                var params;
                if (evt) evt.preventDefault();
                params = this.get_params();
                $.get(this.url, params, this.insert_templated_image_callback);
            },
            'insert_templated_image_callback': function(data, status) {
                window.parent.MediaBrowser.Editor.add_image(data);
            },
            'get_params': function() {                
                var params, action;
                var params = {
                    'display': $("#id_display").val(),
                    'show_caption': $("#id_show_caption").attr("checked") ? "yes" : "no",
                    'show_credit': $("#id_show_credit").attr("checked") ? "yes" : "no"
                }
                action = $("#id_action"); //action field may or may not exist
                if (action.length > 0) params['action'] = action.val();
                return params;
                
            }
        }
    },
    Resize: function() {
        var initial_image_preview, full_size_image, active_image, use_template;
        return {
            'init': function(full_size_img_src) {
                use_template = false;
                initial_image_preview = $("#image-preview").html();
                // Reset options selector
                $($("#resize select option")[0]).attr("selected", "true");         
                var self, url;
                self = this;
                // Observe change in crop options selector:
               var url = full_size_img_src;
               $("#crop-options").change(function() {
                    url = $(this).val()
                    if (url === 'default') { 
                        $("#image-preview").html(initial_image_preview);
                        active_image = full_size_image;
                    }
                    else $.get(url, {}, self.resize_preview_callback);
                });
                // Set full_size_image to full size image:
                $.get(full_size_img_src, {}, function(data) { 
                    active_image = data; 
                    full_size_image = $(data);
                });
                // Fix container image container height and width
                $("#image-preview").css('height', $("#image-preview").height());
                $("#image-preview").css('width', $("#image-preview").width());
                // show_template_fields control
                $("#show_template_fields").attr("checked", false).click(self.template_display)
                // Register form submission behavior:
                $("form#resize button").click(function(evt) {
                    evt.preventDefault();
                    if (use_template) {
                        var params = MediaBrowser.Template().get_params();
                        $.get(url, params, function(data, status) {
                            //this will set active_image:
                            self.resize_preview_callback.apply(self, arguments);
                            // which we then insert into the editor:
                            window.parent.MediaBrowser.Editor.add_image(active_image);
                        });
                        return;
                    }
                    window.parent.MediaBrowser.Editor.add_image(active_image);
                });
            },
            'resize_preview_callback': function(data, status) {    
                active_image = data;
                $("#image-preview").html(data);
                if ($("#image-preview img").width() > $("#image-preview").width()) {
                    $("#image-preview").css('width', $("#image-preview img").width());
                }
                if ($("#image-preview img").height() > $("#image-preview").height()) {
                    $("#image-preview").css('height', $("#image-preview img").height());
                }
            },
            'template_display': function() {
                if ($(this).attr("checked")) {
                    $("#resize fieldset").show();
                    use_template = true;
                }
                else {
                    $("#resize fieldset").hide();
                    use_template = false;
                }

            }
        }
    }(),
    
    _CK_EDITOR: null, 
    
    Editor: function() {
        var dialog_src;
        return {
            dialog: {
                'title': "Image Manager",
                'width': 1200,
                'height': 600,
                'autoOpen': false,
                'draggable': false,
                'modal': true,                
                'position': ['center', 20],
                'resizeable': true
            },
            'init': function(src, opts) {
                var self = this;
                dialog_src = src
                if (arguments[1]) {
                    for (var property in opts) {
                        if (opts.hasOwnProperty(property)) {
                            this.dialog[property] = opts[property];
                        }
                    }
                }
                // Setup JQuery UI dialog:
                $("#dialog").dialog(self.dialog);
                // Register dialog handler:
                $("#browse").click(function(evt) {
                    evt.preventDefault();
                    self.launch_browser();
                });
            },
            'launch_browser': function(editor) {
                //$("#modalIframeId").attr("src","{%url media_browser:image_list%}");
                $("#modalIframeId").attr("src",dialog_src);
                $("#dialog").dialog('open');
                MediaBrowser._CK_EDITOR = editor[0];            
            },
            'add_image': function(tag) {
                if (!tag) return false;
                try {
                    $("#dialog").dialog('close');
                }
                catch (e) { return; } 
                MediaBrowser._CK_EDITOR.insertHtml(tag);
            }
        }
    }()
}