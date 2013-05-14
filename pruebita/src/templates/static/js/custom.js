    jQuery(function(){
        var uploader = new qq.FileUploader({
            element: document.getElementById('file-uploader'),
            action: '/+upload',
			allowedExtensions: [],
			sizeLimit: 0,
			minSizeLimit: 0,
			debug: true,
        });           
    });
