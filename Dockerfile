# Używamy lekkiego obrazu Node.js
FROM node:18-alpine

# Ustawiamy folder roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki definicji zależności
COPY package.json ./

# Instalujemy zależności
RUN npm install

# Kopiujemy resztę kodu aplikacji
COPY . .

# Informujemy Dockera, że kontener używa portu 3000
EXPOSE 3000

# Komenda startowa
CMD ["npm", "start"]
