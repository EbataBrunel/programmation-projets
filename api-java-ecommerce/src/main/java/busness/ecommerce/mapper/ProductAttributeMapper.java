package busness.ecommerce.mapper;

import busness.ecommerce.dto.ProductAttributeResponseDto;
import busness.ecommerce.entity.ProductAttribute;
import org.springframework.stereotype.Component;

@Component
public class ProductAttributeMapper {

    public ProductAttributeResponseDto toDto(ProductAttribute pa) {

        ProductAttributeResponseDto dto = new ProductAttributeResponseDto();

        dto.setId(pa.getId());
        dto.setVariantId(pa.getVariant().getId());
        dto.setAttributeName(
                pa.getAttributeValue().getAttribute().getName()
        );
        dto.setAttributeValue(
                pa.getAttributeValue().getValue()
        );

        return dto;
    }
}

