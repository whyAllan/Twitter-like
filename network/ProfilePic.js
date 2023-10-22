const image = document.getElementById('image-preview');
    const input = document.getElementById('image-upload');
    
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        const reader = new FileReader();

        reader.onload = function(event) {
            image.src = event.target.result;
            const cropper = new Cropper(image, {
                aspectRatio: 1, // Crop to a square shape
                viewMode: 1, // Restrict the crop box to the container
                minCropBoxWidth: 100, // Minimum width of the crop box
                minCropBoxHeight: 100, // Minimum height of the crop box
                responsive: true, // Enable responsive behavior
                // Additional options...
            });
        };

        reader.readAsDataURL(file);
    });