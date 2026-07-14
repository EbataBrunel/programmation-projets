package busness.ecommerce.services;

import busness.ecommerce.dto.ProductImageResponseDto;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface ProductImageService {

    void uploadImages(Long productId, List<MultipartFile> files, Integer mainIndex);

    List<ProductImageResponseDto> getProductImages(Long productId);

    void deleteImage(Long imageId);

    void setMainImage(Long imageId);

    void updateImage(Long imageId, MultipartFile newFile);
}
