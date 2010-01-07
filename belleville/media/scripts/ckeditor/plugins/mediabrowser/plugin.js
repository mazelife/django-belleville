CKEDITOR.plugins.add('mediabrowser',{
    requires: ['iframedialog'],
    init:function(editor){
        CKEDITOR.dialog.addIframe('upload_dialog', 'Image Uploader','path/to/ckeditor/plugins/uploader/dialogs/upload.html',550,400,function(){/*oniframeload*/})
        var cmd = editor.addCommand('mediabrowser', {exec:mediabrowser_onclick})
        cmd.modes={wysiwyg:1,source:1}
        cmd.canUndo=false
        editor.ui.addButton('MediaBrowser',{ label:'Upload an Image..', command:'mediabrowser', icon:this.path+'images/icon.png' })
    }
})

function mediabrowser_onclick(editor)
{
    launch_browser(arguments);
}

/*
CKEDITOR.plugins.add('media_browser', {
    init : function( editor ) {
        var pluginName = 'media_browser';
        // Register the dialog.
        CKEDITOR.dialog.add( pluginName, this.path + 'dialogs/media_browser.js' );
        // Register the command.
        editor.addCommand( pluginName, new CKEDITOR.dialogCommand( pluginName ) );
        // Register the toolbar button.
        editor.ui.addButton( 'Media Browser',
            {
                label : editor.lang.common.image,
                command : pluginName
            });
        // If the "menu" plugin is loaded, register the menu items.
        if ( editor.addMenuItems ) {
            editor.addMenuItems({
                    image : {
                        label : editor.lang.image.menu,
                        command : 'media_browser',
                        group : 'media_browser'
                    }
            });
        }
        // If the "contextmenu" plugin is loaded, register the listeners.
        if ( editor.contextMenu ) {
            editor.contextMenu.addListener( function( element, selection ) {
                if ( !element || !element.is( 'img' ) || element.getAttribute( '_cke_realelement' ) )
                    return null;
                return { image : CKEDITOR.TRISTATE_OFF };
            });
        }
    }
});
/**
 * Whether to remove links when emptying the link URL field in the image dialog.
 * @type Boolean
 * @default true
 * @example
 * config.image_removeLinkByEmptyURL = false;
 */
//CKEDITOR.config.image_removeLinkByEmptyURL = true;
