package busness.ecommerce.mapper;

import busness.ecommerce.dto.BrandRequestDto;
import busness.ecommerce.dto.BrandResponseDto;
import busness.ecommerce.dto.ProductResponseDto;
import busness.ecommerce.entity.Brand;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class BrandMapper {

    public Brand toEntity(BrandRequestDto dto){
        return Brand.builder()
                .name(dto.getName())
                .build();
    }

    public BrandResponseDto toDto(Brand brand){
        return BrandResponseDto.builder()
                .id(brand.getId())
                .name(brand.getName())
                .products(
                        brand.getProducts() == null
                        ? List.of()
                        : brand.getProducts()
                                .stream()
                                .map(product -> ProductResponseDto.builder()
                                        .id(product.getId())
                                        .name(product.getName())
                                        .description(product.getDescription())
                                        .build())
                                .toList()

                )
                .build();
    }
}
