package busness.ecommerce.dto;

import busness.ecommerce.enums.Gender;
import lombok.Data;

import java.util.List;

@Data
public class ProductVariantRequestDto {

    private Long productId;

    private String sku;
    private Double price;
    private Integer stock;
    private Gender gender;

    // ex: [1, 4, 7] → Rouge, M, Coton
    private List<Long> attributes;
}

