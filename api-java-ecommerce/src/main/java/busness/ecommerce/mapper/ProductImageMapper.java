package busness.ecommerce.mapper;

import busness.ecommerce.dto.ProductImageResponseDto;
import busness.ecommerce.entity.ProductImage;
import org.springframework.stereotype.Component;

@Component
public class ProductImageMapper {

    public ProductImageResponseDto toDto(ProductImage image) {
        return ProductImageResponseDto.builder()
                .id(image.getId())
                .url(image.getUrl())
                .mainImage(image.isMainImage())
                .build();
    }
}
