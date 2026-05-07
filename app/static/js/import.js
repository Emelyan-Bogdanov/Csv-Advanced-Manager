const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const clearFileBtn = document.getElementById('clearFileBtn');
        const uploadForm = document.getElementById('uploadForm');
        const errorMessage = document.getElementById('errorMessage');
        const successMessage = document.getElementById('successMessage');
        const submitBtn = document.getElementById('submitBtn');
        const loadingText = document.getElementById('loadingText');
        const submitText = document.getElementById('submitText');

        // Click to select file
        uploadArea.addEventListener('click', () => fileInput.click());

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });

        // File input change
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });

        // Handle file selection
        function handleFileSelect(file) {
            clearMessages();

            // Validate file size (max 50MB)
            const maxSize = 50 * 1024 * 1024;
            if (file.size > maxSize) {
                showError('File size must be less than 50MB');
                fileInput.value = '';
                return;
            }

            // Display file info
            fileName.textContent = file.name;
            fileSize.textContent = `${(file.size / 1024).toFixed(2)} KB`;
            fileInfo.classList.add('show');
            uploadArea.style.opacity = '0.5';
        }

        // Clear file selection
        clearFileBtn.addEventListener('click', () => {
            fileInput.value = '';
            fileInfo.classList.remove('show');
            uploadArea.style.opacity = '1';
            clearMessages();
        });

        // Form submission
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (fileInput.files.length === 0) {
                showError('Please select a file');
                return;
            }

            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);

            // Show loading state
            submitBtn.disabled = true;
            loadingText.classList.add('show');
            submitText.style.display = 'none';

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    showSuccess(`Dataset "${file.name}" imported successfully! (${data.total_rows} rows)`);
                    fileInput.value = '';
                    fileInfo.classList.remove('show');
                    uploadArea.style.opacity = '1';
                    
                    // Optional: Redirect after success
                    setTimeout(() => {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        }
                    }, 1500);
                } else {
                    showError(data.error || 'Failed to import dataset');
                }
            } catch (error) {
                showError('Error uploading file. Please try again.');
                console.error('Upload error:', error);
            } finally {
                submitBtn.disabled = false;
                loadingText.classList.remove('show');
                submitText.style.display = 'inline';
            }
        });

        // Message handlers
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.classList.add('show');
            successMessage.classList.remove('show');
        }

        function showSuccess(message) {
            successMessage.textContent = message;
            successMessage.classList.add('show');
            errorMessage.classList.remove('show');
        }

        function clearMessages() {
            errorMessage.classList.remove('show');
            successMessage.classList.remove('show');
        }