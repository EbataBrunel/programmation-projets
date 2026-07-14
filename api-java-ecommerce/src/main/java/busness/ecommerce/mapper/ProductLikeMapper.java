package busness.ecommerce.mapper;

import busness.ecommerce.dto.ProductLikeRequestDto;
import busness.ecommerce.dto.ProductLikeResponseDto;
import busness.ecommerce.entity.ProductLike;
import busness.ecommerce.entity.ProductVariant;
import busness.ecommerce.entity.User;
import org.springframework.stereotype.Component;

@Component
public class ProductLikeMapper {

    public ProductLike toEntity(ProductLikeRequestDto dto, User user, ProductVariant variant){
        return ProductLike.builder()
                .user(user)
                .variant(variant)
                .build();
    }

    public ProductLikeResponseDto toDto(ProductLike like){
        return ProductLikeResponseDto.builder()
                .id(like.getId())
                .userId(like.getId())
                .variantId(like.getId())
                .build();
    }
}
