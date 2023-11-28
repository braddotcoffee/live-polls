# 👩‍💻 Contributing

Right now Twitch Live Polls is not actively seeking new contributors. That being said, the right PR will always get merged 😎.

## Development Setup
The development setup guide is quite similar to the Quickstart that is [found in the README](../README.md)

Copy the example config into a `config.yaml` for use with the development Docker Compose configuration
```bash
cd backend
cp config-example.yaml config.yaml
```

**Edit the example config to point to your Twitch channel.** This can be found under `Voting > ChannelName`.

Copy the example secrets file into `secrets.yaml` for use with the development Docker Compose configuration
```bash
cp secrets-example.yaml secret.yaml
```

**Edit the file to include a LONG and RANDOM token for authenticating to your server endpoints**. This can be found under `Server > Token`.

Spin up the Docker Compose. The service will now be listening on `localhost:3000`.
```bash
docker compose up
```

### Frontend Setup
Create a .env file that points at your backend for the `NEXT_PUBLIC_API_URL`
```bash
cd ..
cd frontend
echo 'NEXT_PUBLIC_API_URL="localhost:3000"' > .env
```

Run the NextJS development command. The app will be served on `localhost:4200`.
```bash
npm run dev
```
