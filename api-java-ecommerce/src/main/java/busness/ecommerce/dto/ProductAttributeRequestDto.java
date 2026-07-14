package busness.ecommerce.dto;

import lombok.Data;

@Data
public class ProductAttributeRequestDto {
    private Long variantId;
    private Long attributeValueId;
}
