package busness.ecommerce.dto;

import lombok.Data;

@Data
public class ProductAttributeResponseDto {
    private Long id;

    private Long variantId;

    private String attributeName;
    private String attributeValue;
}
