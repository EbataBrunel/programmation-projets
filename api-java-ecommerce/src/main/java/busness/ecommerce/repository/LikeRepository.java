package busness.ecommerce.repository;

import busness.ecommerce.dto.VariantLikeUserDto;
import busness.ecommerce.entity.ProductLike;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface LikeRepository extends JpaRepository<ProductLike, Long> {
    boolean existsByUserIdAndVariantId(Long userId, Long variantId);
    Optional<ProductLike> findByUserIdAndVariantId(Long userId, Long variantId);

    @Query("""
        SELECT pl FROM ProductLike pl
        JOIN FETCH pl.variant v
        JOIN FETCH v.product p
        LEFT JOIN FETCH p.images
        WHERE pl.user.id = :userId
    """)
    List<ProductLike> findLikedVariantsByUserId(@Param("userId") Long userId);

    @Query("""
        SELECT new busness.ecommerce.dto.VariantLikeUserDto(
            u.id,
            up.firstName,
            up.lastName
        )
        FROM ProductLike pl
        JOIN pl.user u
        JOIN UserProfile up ON up.user.id = u.id
        WHERE pl.variant.id = :variantId
    """)
    List<VariantLikeUserDto> findUsersWhoLikedVariant(Long variantId);
}
