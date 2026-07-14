package busness.ecommerce.services;
import org.springframework.web.multipart.MultipartFile;

public interface FileStorageService {

    String saveFile(MultipartFile file);

    void deleteFile(String filename);
}

