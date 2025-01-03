from django import forms
from django.forms.widgets import Widget, FileInput
from django.utils.safestring import mark_safe
from django.db import models

class CaptureWidget(Widget):
    allow_multiple_selected = False
    template_name = 'widgets/capture-field.html'

    def format_value(self, value):
        """File input never renders a value."""
        return

    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        getter = files.get
        if self.allow_multiple_selected:
            try:
                getter = files.getlist
            except AttributeError:
                pass
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        return name not in files

    def use_required_attribute(self, initial):
        return super().use_required_attribute(initial) and not initial

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context['widget'].update({
            'verbose_name': self.attrs.get('verbose_name', name),
            'value': value if value else '',
        })
        return mark_safe(renderer.render(self.template_name, context))

    @property
    def media(self):
        return forms.Media(js=[mark_safe(self.get_js_script())])

    def get_js_script(self):
        return '''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const containers = document.querySelectorAll('.webcam-capture-container');

            containers.forEach(container => {
                const videoId = container.querySelector('video').id;
                const captureId = container.querySelector('button.capture').id;
                const canvasId = container.querySelector('canvas').id;
                const inputId = container.querySelector('input[type="file"]').id;
                const deviceSelectId = container.querySelector('select').id;
                const retakeId = container.querySelector('button.retake').id;

                const video = document.getElementById(videoId);
                const canvas = document.getElementById(canvasId);
                const captureButton = document.getElementById(captureId);
                const imageInput = document.getElementById(inputId);
                const deviceSelect = document.getElementById(deviceSelectId);
                const retakeButton = document.getElementById(retakeId);

                const existingValue = $(imageInput).data('url');

                let stream;

                function startVideo(deviceId) {
                    const constraints = {
                        video: deviceId ? {deviceId: {exact: deviceId}} : true
                    };

                    navigator.mediaDevices.getUserMedia(constraints)
                        .then(newStream => {
                            stream = newStream;
                            video.srcObject = stream;
                            video.style.display = 'block';
                            canvas.style.display = 'none';
                            captureButton.style.display = 'inline-block';
                            retakeButton.style.display = 'none';
                        })
                        .catch(err => {
                            console.error("Error accessing the webcam", err);
                        });
                }

                function stopVideo() {
                    if (stream) {
                        stream.getTracks().forEach(track => track.stop());
                    }
                }

                navigator.mediaDevices.enumerateDevices()
                    .then(devices => {
                        const videoDevices = devices.filter(device => device.kind === 'videoinput');
                        videoDevices.forEach(device => {
                            const option = document.createElement('option');
                            option.value = device.deviceId;
                            option.text = device.label || `Camera ${deviceSelect.length + 1}`;
                            deviceSelect.appendChild(option);
                        });
                        if (videoDevices.length > 0 && !existingValue) {
                            startVideo(videoDevices[0].deviceId);
                        }
                    });

                deviceSelect.addEventListener('change', (event) => {
                    stopVideo();
                    startVideo(event.target.value);
                });

                captureButton.addEventListener('click', () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    stopVideo();
                    video.style.display = 'none';
                    canvas.style.display = 'block';
                    captureButton.style.display = 'none';
                    retakeButton.style.display = 'inline-block';
                    canvas.toBlob(blob => {
                        const file = new File([blob], "webcam-photo.jpg", { type: "image/jpeg" });
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(file);
                        imageInput.files = dataTransfer.files;
                    }, 'image/jpeg');
                });

                retakeButton.addEventListener('click', () => {
                    startVideo(deviceSelect.value);
                });

                // Show existing image in canvas if present
                if (existingValue) {
                    const img = new Image();
                    img.onload = function() {
                        canvas.width = img.width;
                        canvas.height = img.height;
                        canvas.getContext('2d').drawImage(img, 0, 0);
                        video.style.display = 'none';
                        canvas.style.display = 'block';
                        captureButton.style.display = 'none';
                        retakeButton.style.display = 'inline-block';
                    };
                    img.src = existingValue;
                }
            });
        });
        </script>
        '''
        
class CaptureField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.pop('level', 0)
        self.inline = kwargs.pop('inline', False)
        
        super().__init__(*args, **kwargs)
        
    def formfield(self, **kwargs):
        kwargs['widget'] = CaptureWidget
        return super().formfield(**kwargs)
