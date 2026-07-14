package busness.ecommerce.services;

import busness.ecommerce.dto.ProductImageResponseDto;
import busness.ecommerce.entity.Product;
import busness.ecommerce.entity.ProductImage;
import busness.ecommerce.mapper.ProductImageMapper;
import busness.ecommerce.repository.ProductImageRepository;
import busness.ecommerce.repository.ProductRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
@AllArgsConstructor
public class ProductImageServiceImpl implements ProductImageService {

    private final ProductRepository productRepository;
    private final ProductImageRepository productImageRepository;
    private final FileStorageService fileStorageService;
    private final ProductImageMapper productImageMapper;

    @Override
    public void uploadImages(Long productId,
                             List<MultipartFile> files,
                             Integer mainIndex) {

        Product product = productRepository.findById(productId)
                .orElseThrow(() ->
                        new RuntimeException("Product not found"));

        for (int i = 0; i < files.size(); i++) {

            String filename = fileStorageService.saveFile(files.get(i));

            ProductImage image = new ProductImage();
            image.setUrl(filename);
            image.setMainImage(mainIndex != null && i == mainIndex);
            image.setProduct(product);

            productImageRepository.save(image);
        }
    }

    @Override
    public List<ProductImageResponseDto> getProductImages(Long productId) {
        return productImageRepository.findByProductId(productId)
                .stream()
                .map(productImageMapper::toDto)
                .toList();
    }

    @Override
    public void deleteImage(Long imageId) {
        ProductImage image = productImageRepository.findById(imageId)
                .orElseThrow(() -> new RuntimeException("Image not found"));

        fileStorageService.deleteFile(image.getUrl());

        productImageRepository.delete(image);
    }

    @Override
    public void setMainImage(Long imageId) {
        ProductImage image = productImageRepository.findById(imageId)
                .orElseThrow();

        Long productId = image.getProduct().getId();

        // désactiver toutes les images principales
        productImageRepository.findByProductId(productId)
                .forEach(img -> {
                    img.setMainImage(false);
                    productImageRepository.save(img);
                });

        image.setMainImage(true);
        productImageRepository.save(image);
    }

    @Override
    public void updateImage(Long imageId, MultipartFile newFile) {

        ProductImage image = productImageRepository.findById(imageId)
                .orElseThrow(() -> new RuntimeException("Image not found"));

        // Supprimer l'ancien fichier si nécessaire
        fileStorageService.deleteFile(image.getUrl());

        // Sauvegarder le nouveau fichier
        String newFilename = fileStorageService.saveFile(newFile);

        image.setUrl(newFilename);

        productImageRepository.save(image);
    }
}

