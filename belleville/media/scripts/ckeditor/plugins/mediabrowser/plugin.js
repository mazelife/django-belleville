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

function mediabrowser_onclick(editor) {
    MediaBrowser.Editor.launch_browser(arguments);
}