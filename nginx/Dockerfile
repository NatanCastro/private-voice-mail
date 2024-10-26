FROM nginx:alpine

# Copy NGINX configuration to the container
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create directories for audio files
RUN mkdir -p /usr/share/nginx/html/audio_files && \
  mkdir -p /tmp/incoming && \
  chown nginx -R /usr/share/nginx/html/audio_files && \
  chown nginx:nginx -R /tmp/incoming && \
  chmod -R 777 /usr/share/nginx/html/audio_files
