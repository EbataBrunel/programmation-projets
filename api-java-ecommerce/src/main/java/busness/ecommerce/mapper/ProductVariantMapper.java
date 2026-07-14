package busness.ecommerce.mapper;

import busness.ecommerce.dto.ProductLikeResponseDto;
import busness.ecommerce.dto.ProductVariantResponseDto;
import busness.ecommerce.entity.ProductVariant;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
public class ProductVariantMapper {

    private final ProductMapper productMapper;

    public ProductVariantResponseDto toDto(ProductVariant variant) {

        ProductVariantResponseDto dto = new ProductVariantResponseDto();

        dto.setId(variant.getId());
        dto.setSku(variant.getSku());
        dto.setPrice(variant.getPrice());
        dto.setStock(variant.getStock());
        dto.setGender(variant.getGender());
        dto.setProduct(productMapper.toDto(variant.getProduct()));
        List<String> attributes =
                (variant.getAttributes() == null
                ? List.of()
                :variant.getAttributes()
                        .stream()
                        .map(pa ->
                                pa.getAttributeValue().getAttribute().getName()
                                        + ": "
                                        + pa.getAttributeValue().getValue()
                        )
                        .toList());

        dto.setAttributes(attributes);

        return dto;
    }

}
