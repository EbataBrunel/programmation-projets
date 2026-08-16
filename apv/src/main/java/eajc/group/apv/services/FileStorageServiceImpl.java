package eajc.group.apv.services;

import com.cloudinary.Cloudinary;
import com.cloudinary.utils.ObjectUtils;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;
import java.util.UUID;

@Service
public class FileStorageServiceImpl implements FileStorageService {

    private final Cloudinary cloudinary;

    public FileStorageServiceImpl(Cloudinary cloudinary) {
        this.cloudinary = cloudinary;
    }

    @Override
    public String saveFile(MultipartFile file) {

        if (file == null || file.isEmpty()) {
            return null;
        }

        try {

            String originalName = file.getOriginalFilename();

            String extension = "";

            if (originalName != null && originalName.contains(".")) {
                extension = originalName.substring(
                        originalName.lastIndexOf(".")
                );
            }

            String publicId = UUID.randomUUID().toString();

            Map<?, ?> result = cloudinary.uploader().upload(
                    file.getBytes(),
                    ObjectUtils.asMap(
                            "public_id", publicId,
                            "resource_type", "auto"
                    )
            );

            return (String) result.get("secure_url");

        } catch (IOException e) {
            throw new RuntimeException(
                    "Erreur upload fichier vers Cloudinary",
                    e
            );
        }
    }

    @Override
    public void deleteFile(String filename) {

        if (filename == null || filename.isBlank()) {
            return;
        }

        try {

            // Si filename contient l'URL Cloudinary,
            // on récupère le public_id.
            String publicId = extractPublicId(filename);

            cloudinary.uploader().destroy(
                    publicId,
                    ObjectUtils.emptyMap()
            );

        } catch (Exception e) {
            throw new RuntimeException(
                    "Erreur suppression fichier Cloudinary",
                    e
            );
        }
    }
    @Override
    public String extractPublicId(String url) {

        try {

            String path = new java.net.URI(url).getPath();

            // Exemple :
            // /xxx/image/upload/v123/abc.jpg

            int uploadIndex = path.indexOf("/upload/");

            if (uploadIndex == -1) {
                return url;
            }

            String publicPath =
                    path.substring(uploadIndex + "/upload/".length());

            // Supprimer v123/
            if (publicPath.startsWith("v")) {

                int slashIndex = publicPath.indexOf("/");

                if (slashIndex > 0) {
                    publicPath =
                            publicPath.substring(slashIndex + 1);
                }
            }

            // Supprimer extension
            int dotIndex = publicPath.lastIndexOf(".");

            if (dotIndex > 0) {
                publicPath =
                        publicPath.substring(0, dotIndex);
            }

            return publicPath;

        } catch (Exception e) {
            return url;
        }
    }
}