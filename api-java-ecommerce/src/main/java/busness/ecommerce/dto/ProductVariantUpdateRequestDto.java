package busness.ecommerce.dto;

import busness.ecommerce.enums.Gender;
import lombok.Data;

@Data
public class ProductVariantUpdateRequestDto {
    private Double price;
    private Integer stock;
    private Gender gender;
}

