package busness.ecommerce.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Service
public class FileStorageServiceImpl implements FileStorageService{
    @Value("${file.upload-dir}")
    private String uploadDir;

    public String saveFile(MultipartFile file) {

        try {
            // créer le dossier s'il n'existe pas
            Path uploadPath = Paths.get(uploadDir);
            if (!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }

            // nom unique
            String originalName = file.getOriginalFilename();
            String extension = originalName.substring(originalName.lastIndexOf("."));
            String filename = UUID.randomUUID() + extension;

            // chemin final
            Path filePath = uploadPath.resolve(filename);

            // sauvegarde
            Files.copy(file.getInputStream(), filePath);

            return filename;

        } catch (Exception e) {
            throw new RuntimeException("Erreur upload fichier", e);
        }
    }

    public void deleteFile(String filename) {
        Path path = Paths.get(uploadDir).resolve(filename);

        try {
            if (Files.exists(path)) {
                Files.delete(path);
            }
        } catch (IOException e) {
            throw new RuntimeException("Failed to delete file: " + filename, e);
        }
    }
}
