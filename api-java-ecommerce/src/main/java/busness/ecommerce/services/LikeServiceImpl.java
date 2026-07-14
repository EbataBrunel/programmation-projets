package busness.ecommerce.services;

import busness.ecommerce.dto.LikedVariantResponseDto;
import busness.ecommerce.dto.ProductLikeRequestDto;
import busness.ecommerce.dto.ProductLikeResponseDto;
import busness.ecommerce.dto.VariantLikeUserDto;
import busness.ecommerce.entity.Product;
import busness.ecommerce.entity.ProductLike;
import busness.ecommerce.entity.ProductVariant;
import busness.ecommerce.entity.User;
import busness.ecommerce.mapper.ProductLikeMapper;
import busness.ecommerce.repository.LikeRepository;
import busness.ecommerce.repository.ProductVariantRepository;
import busness.ecommerce.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class LikeServiceImpl implements LikeService{

    private final LikeRepository likeRepository;
    private final ProductLikeMapper likeMapper;
    private final UserRepository userRepository;
    private final ProductVariantRepository productVariantRepository;

    @Override
    public ProductLikeResponseDto addLike(ProductLikeRequestDto dto) {
        User user = userRepository.findById(dto.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        ProductVariant variant = productVariantRepository.findById(dto.getVariantId())
                .orElseThrow(() -> new RuntimeException("Variant not found"));

        ProductLike like = likeMapper.toEntity(dto, user, variant);
        ProductLike likeSave = likeRepository.save(like);

        return likeMapper.toDto(likeSave);
    }

    @Override
    public boolean existsByUserIdAndVariantId(Long userId, Long variantId) {
        return likeRepository.existsByUserIdAndVariantId(userId, variantId);
    }

    @Override
    public ProductLikeResponseDto getLike(Long userId, Long variantId) {
            ProductLike productLike = likeRepository.findByUserIdAndVariantId(userId, variantId)
                .orElse(null); // ou throw exception
        return likeMapper.toDto(productLike);
    }

    @Override
    public boolean toggleLike(Long userId, Long variantId) {

        Optional<ProductLike> existing =
                likeRepository.findByUserIdAndVariantId(userId, variantId);

        if (existing.isPresent()) {
            likeRepository.delete(existing.get());
            return false;
        } else {
            ProductLike like = ProductLike.builder()
                    .user(userRepository.getReferenceById(userId))
                    .variant(productVariantRepository.getReferenceById(variantId))
                    .build();

            likeRepository.save(like);
            return true;
        }
    }

    @Override
    public List<LikedVariantResponseDto> getLikedVariants(Long userId) {
        return likeRepository.findLikedVariantsByUserId(userId)
                .stream()
                .map(pl -> {

                    ProductVariant variant = pl.getVariant();
                    Product product = variant.getProduct();

                    String imageUrl = product.getImages()
                            .stream()
                            .filter(img -> Boolean.TRUE.equals(img.isMainImage()))
                            .map(img -> img.getUrl())
                            .findFirst()
                            .orElse(null);

                    return LikedVariantResponseDto.builder()
                            .variantId(variant.getId())
                            .productName(product.getName())
                            .sku(variant.getSku())
                            .price(variant.getPrice())
                            .imageUrl(imageUrl)
                            .build();
                })
                .toList();
    }

    @Override
    public List<VariantLikeUserDto> getUsersWhoLiked(Long variantId) {
        return likeRepository.findUsersWhoLikedVariant(variantId);
    }

    @Override
    public void deleteLike(Long id) {
        ProductLike like = likeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("ProductLike not found"));
        likeRepository.delete(like);
    }
}
