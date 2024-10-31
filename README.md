# Projet Streamlit de Génération de Vidéos

## Description

Ce projet utilise Streamlit pour créer une application web permettant de générer des vidéos à partir de fichiers audio et d'images, en utilisant l'API OpenAI pour optimiser le contenu. Il utilise également l'API Eleven Labs pour la synthèse vocale.

## Fonctionnalités

- **Génération de Vidéos** : Créez des vidéos en combinant du texte, des images et des fichiers audio.
- **Synthèse Vocale** : Générez des voix de haute qualité à partir de texte avec Eleven Labs.
- **Interface Utilisateur Intuitive** : Utilisation simplifiée avec des boutons pour interagir facilement avec les fonctionnalités.

## Technologies Utilisées

- **Streamlit** : Framework web pour Python.
- **OpenAI** : API pour la génération de texte et la transcription audio.
- **Eleven Labs** : API pour la synthèse vocale.
- **MoviePy** : Bibliothèque pour la manipulation de vidéos.
- **Requests** : Pour effectuer des requêtes HTTP.
- **Python-dotenv** : Pour gérer les variables d'environnement.

## Prérequis

Assurez-vous d'avoir Python 3.7 ou supérieur installé. 

## Configuration

1. Clonez le dépôt :

```
git clone https://github.com/tucommenceapousser/TrknTikTokUp cd TrknTikTokUp
```

2. Créez un fichier `.env.toml` à la racine de votre projet et ajoutez vos clés API :

```
OPENAI_API_KEY = ""
ELEVEN_LABS_API_KEY = ""
```

## Utilisation

1. Démarrez l'application Streamlit :

```
streamlit run app.py
```

2. Ouvrez votre navigateur et allez à `http://localhost:8501`.

3. Téléchargez votre fichier audio ou vidéo, ajoutez un thème d'image et une description, puis cliquez sur le bouton pour générer votre vidéo.

## Screenshots

Voici quelques captures d'écran de l'application :

![Screenshot 1](path_to_screenshot1.png)  
![Screenshot 2](path_to_screenshot2.png)

## Contribuer

Si vous souhaitez contribuer à ce projet, n'hésitez pas à ouvrir une issue ou à soumettre une demande de tirage.

## Auteurs

TRHACKNON - [GitHub](https://github.com/tucommenceapousser)

## License

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier LICENSE.

