# Берём лёгкий nginx
FROM nginx:alpine

# Кладём все файлы сайта в стандартную папку nginx
COPY . /usr/share/nginx/html

# Открываем порт 80
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]
