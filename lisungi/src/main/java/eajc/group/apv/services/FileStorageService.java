package eajc.group.apv.services;
import org.springframework.web.multipart.MultipartFile;

public interface FileStorageService {

    String saveFile(MultipartFile file);

    void deleteFile(String filename);
}

