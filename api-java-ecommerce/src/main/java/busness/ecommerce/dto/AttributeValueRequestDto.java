package busness.ecommerce.dto;


import lombok.Data;

@Data
public class AttributeValueRequestDto {
    private String value;
    private Long attributeId;
}

