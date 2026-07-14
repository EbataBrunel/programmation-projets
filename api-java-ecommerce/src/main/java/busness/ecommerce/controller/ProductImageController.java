package busness.ecommerce.controller;

import busness.ecommerce.dto.ProductImageResponseDto;
import busness.ecommerce.services.ProductImageService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@CrossOrigin(origins = "http://localhost:4200")
@RestController
@RequestMapping("/api/v1/product-images")
@RequiredArgsConstructor
public class ProductImageController {

    private final ProductImageService productImageService;

    @PostMapping("/{productId}")
    public void uploadImages(
            @PathVariable Long productId,
            @RequestParam("files") List<MultipartFile> files,
            @RequestParam(required = false) Integer mainIndex
    ) {
        productImageService.uploadImages(productId, files, mainIndex);
    }

    @GetMapping("/{productId}")
    public List<ProductImageResponseDto> getImages(
            @PathVariable Long productId) {
        return productImageService.getProductImages(productId);
    }

    @DeleteMapping("/{imageId}")
    public void deleteImage(@PathVariable Long imageId) {
        productImageService.deleteImage(imageId);
    }

    @PutMapping("/main/{imageId}")
    public void setMainImage(@PathVariable Long imageId) {

        productImageService.setMainImage(imageId);
    }

    @PatchMapping(value = "/{imageId}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<?> updateImage(
            @PathVariable Long imageId,
            @RequestPart("file") MultipartFile file) {

        productImageService.updateImage(imageId, file);
        return ResponseEntity.ok().build();
    }
}
