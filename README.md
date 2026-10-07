services:
  mongodb:
    image: mongo:latest
    container_name: majors-mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: password123
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

  geth:
    image: ethereum/client-go:latest
    container_name: majors-geth
    command: >
      --http
      --http.addr 0.0.0.0
      --http.vhosts "*"
      --http.api eth,net,web3,txpool,personal,admin
      --ws
      --ws.addr 0.0.0.0
      --ws.origins "*"
      --rpcvhosts "*"
      --syncmode full
      --datadir /data
    ports:
      - "8545:8545"
      - "8546:8546"
    volumes:
      - geth_data:/data
    restart: unless-stopped

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: majors-api
    environment:
      MONGODB_URL: mongodb://root:password123@mongodb:27017/majors?authSource=admin
      ETHEREUM_RPC_URL: http://geth:8545
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - geth
    restart: unless-stopped

volumes:
  mongodb_data:
  geth_data:
