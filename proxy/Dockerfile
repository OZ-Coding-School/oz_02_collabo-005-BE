FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY okivery.conf /etc/nginx/sites-enabled/
CMD ["nginx", "-g", "daemon off;"]