package busness.ecommerce.services;

import busness.ecommerce.dto.LikedVariantResponseDto;
import busness.ecommerce.dto.ProductLikeRequestDto;
import busness.ecommerce.dto.ProductLikeResponseDto;
import busness.ecommerce.dto.VariantLikeUserDto;

import java.util.List;

public interface LikeService {
    // CREATE
    ProductLikeResponseDto addLike(ProductLikeRequestDto dto);
    // GET
    boolean existsByUserIdAndVariantId(Long userId, Long variantId);
    // GET
    ProductLikeResponseDto getLike(Long userId, Long variantId);
    // GET
    boolean toggleLike(Long userId, Long variantId);
    // GET
    List<LikedVariantResponseDto> getLikedVariants(Long userId);
    // GET
    List<VariantLikeUserDto> getUsersWhoLiked(Long variantId);
    // DELETE
    void deleteLike(Long id);
}
