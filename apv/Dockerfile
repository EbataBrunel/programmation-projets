# ============================================================
# ÉTAPE 1 : CONSTRUIRE (compiler) l'application Spring Boot
# ============================================================

# On utilise une image qui contient :
# - Maven 3.9
# - Java 17 (Eclipse Temurin)
# - Alpine Linux (distribution Linux légère)
#
# "AS build" donne le nom "build" à cette étape.
FROM maven:3.9-eclipse-temurin-17-alpine AS build


# Définit le dossier de travail à l'intérieur du conteneur.
# À partir de maintenant, les commandes seront exécutées
# depuis /app.
WORKDIR /app


# Copie le fichier pom.xml de ton ordinateur
# vers /app dans le conteneur.
#
# Ton projet local :
#   mon-projet/pom.xml
#
# devient dans le conteneur :
#   /app/pom.xml
COPY pom.xml .


# Copie le dossier src de ton projet
# vers /app/src dans le conteneur.
#
# Ton projet local :
#   mon-projet/src/
#
# devient :
#   /app/src/
COPY src ./src


# Lance Maven pour compiler ton application.
#
# clean  -> supprime les anciennes compilations
# package -> compile le projet et crée le fichier .jar
# -DskipTests -> ne lance pas les tests pendant le build
#
# Le .jar sera créé dans :
# /app/target/
RUN mvn clean package -DskipTests


# ============================================================
# ÉTAPE 2 : EXÉCUTER l'application
# ============================================================

# On utilise une nouvelle image contenant uniquement :
# - Java 17
# - le JRE (Java Runtime Environment)
# - Alpine Linux
#
# IMPORTANT :
# Maven n'est plus nécessaire ici.
FROM eclipse-temurin:17-jre-alpine


# Définit /app comme dossier de travail.
WORKDIR /app


# Récupère le fichier .jar créé dans l'étape précédente.
#
# --from=build signifie :
# "va chercher le fichier dans l'étape appelée build"
#
# Le fichier :
# /app/target/*.jar
#
# sera copié vers :
# /app/app.jar
COPY --from=build /app/target/*.jar app.jar


# Indique que l'application utilise le port 8080.
#
# Attention :
# EXPOSE ne démarre PAS le port.
# C'est principalement une information/documentation
# pour Docker.
EXPOSE 8080


# Commande exécutée lorsque le conteneur démarre.
#
# Cela revient à exécuter :
# java -jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]