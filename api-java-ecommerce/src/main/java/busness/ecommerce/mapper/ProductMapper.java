package busness.ecommerce.mapper;

import busness.ecommerce.dto.ProductImageResponseDto;
import busness.ecommerce.dto.ProductRequestDto;
import busness.ecommerce.dto.ProductResponseDto;
import busness.ecommerce.dto.UserResponseDto;
import busness.ecommerce.entity.*;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class ProductMapper {
    public Product toEntity(
            ProductRequestDto dto,
            Category category,
            SubCategory subCategory,
            ProductCategory productCategory,
            User owner,
            Brand brand) {

        return Product.builder()
                .name(dto.getName())
                .description(dto.getDescription())
                .price(dto.getPrice())
                .source(dto.getSource())
                .subCategory(subCategory)
                .category(category)
                .productCategory(productCategory)
                .owner(owner)
                .brand(brand)
                .build();
    }

    public ProductResponseDto toDto(Product product) {

        return ProductResponseDto.builder()
                .id(product.getId())
                .name(product.getName())
                .description(product.getDescription())
                .price(product.getPrice())
                .source(product.getSource())
                .categoryId(
                        product.getCategory() != null
                                ?product.getCategory().getId()
                                : null
                )
                .subCategoryId(
                        product.getSubCategory() != null
                            ?product.getSubCategory().getId()
                            : null
                )
                .productCategoryId(
                        product.getProductCategory() != null
                                ? product.getProductCategory().getId()
                                : null
                )
                .brandId(
                        product.getBrand() != null
                        ? product.getBrand().getId()
                        : null
                )
                .brandName(
                        product.getBrand() !=null
                        ? product.getBrand().getName()
                        : null
                )
                .ownerId(
                        product.getOwner() != null
                        ? product.getOwner().getId()
                        : null
                )
                .images(
                        product.getImages() == null
                        ? List.of()
                        : product.getImages()
                                .stream()
                                .map(img -> ProductImageResponseDto.builder()
                                        .id(img.getId())
                                        .mainImage(img.isMainImage())
                                        .url(img.getUrl())
                                        .build())
                                .toList()
                )
                .build();
    }
}
