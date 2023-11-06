const image = document.getElementById('image-preview');
        const input = document.getElementById('image-upload');
        const saveButton = document.querySelector('.btn-save');
        const picInput = document.getElementById('pic');
        const alertMessage = document.querySelector('.alert');

        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const reader = new FileReader();

            reader.onload = function(event) {
                image.src = event.target.result;
                const cropper = new Cropper(image, {
                    aspectRatio: 1, // Crop to a square shape
                    viewMode: 1, // Restrict the crop box to the container
                    minCropBoxWidth: 300, // Minimum width of the crop box
                    minCropBoxHeight: 300, // Minimum height of the crop box
                    responsive: true, // Enable responsive behavior
                });

                saveButton.addEventListener('click', function() {
                    const croppedCanvas = cropper.getCroppedCanvas();
                    const croppedImageDataUrl = croppedCanvas.toDataURL('image/jpeg');
                    picInput.value = croppedImageDataUrl;
                    alertMessage.textContent = 'Image uploaded successfully!';
                    alertMessage.style.display = 'block';
                });
            };

            reader.readAsDataURL(file);
        });