package busness.ecommerce.dto;

import busness.ecommerce.enums.Gender;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class ProductVariantResponseDto {

    private Long id;
    private String sku;
    private Double price;
    private Integer stock;
    private Gender gender;
    private ProductResponseDto product;

    private List<String> attributes;
}

