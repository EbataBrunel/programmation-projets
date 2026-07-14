package busness.ecommerce.repository;

import busness.ecommerce.entity.ProductCategory;
import busness.ecommerce.enums.Gender;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ProductCategoryRepository extends JpaRepository<ProductCategory, Long> {
    List<ProductCategory> findBySubCategoryId(Long subCategoryId);
    @Query("""
            SELECT pc.id as productCategoryId,
                    pc.name as productCategoryName,
                    COUNT(pc.id) as variantCount
            FROM ProductVariant pv
            JOIN pv.product p
            JOIN p.productCategory pc
            WHERE pv.gender = :gender
            AND p.subCategory.id = :subCategoryId
            GROUP by pc.id, pc.name
            """)
    List<Object[]> countVariantsProductCategoryByGenderAndSubCategory(
            @Param("gender") Gender gender,
            @Param("subCategoryId") Long subCategoryId
    );
}
