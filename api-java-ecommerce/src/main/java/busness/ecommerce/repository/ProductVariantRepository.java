package busness.ecommerce.repository;

import busness.ecommerce.entity.ProductVariant;
import busness.ecommerce.enums.Gender;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;


import java.util.List;

public interface ProductVariantRepository extends JpaRepository<ProductVariant, Long> {

    List<ProductVariant> findByProductId(Long productId);

    List<ProductVariant> findTop3ByProduct_ProductCategory_IdAndGender(
            Long productCategoryId,
            Gender gender
    );

    Page<ProductVariant> findByGenderAndProduct_Brand_IdIn(
            Gender gender,
            List<Long> brandIds,
            Pageable pageable
    );

    Page<ProductVariant> findByGenderAndProduct_Category_IdAndProduct_Brand_IdIn(
            Gender gender,
            Long categoryId,
            List<Long> brandIds,
            Pageable pageable
    );

    Page<ProductVariant> findByGenderAndProduct_SubCategory_IdAndProduct_Brand_IdIn(
            Gender gender,
            Long subCategoryId,
            List<Long> brandIds,
            Pageable pageable
    );


    Page<ProductVariant> findByGenderAndProduct_ProductCategory_IdAndProduct_Brand_IdIn(
            Gender gender,
            Long productCategoryId,
            List<Long> brandIds,
            Pageable pageable
    );

    @Query("""
        SELECT pv
        FROM ProductVariant pv
        JOIN pv.product p
        WHERE pv.gender = :gender
        AND p.subCategory.id = :subCategoryId
    """)
    Page<ProductVariant> findByGenderAndCategoryAndSubCategory(
            @Param("gender") Gender gender,
            @Param("subCategoryId") Long subCategoryId,
            Pageable pageable
    );

    @Query("""
        SELECT pv
        FROM ProductVariant pv
        WHERE pv.gender = :gender
    """)
    Page<ProductVariant> findByGender(
            @Param("gender") Gender gender,
            Pageable pageable
    );

    @Query("""
        SELECT pv
        FROM ProductVariant pv
        JOIN pv.product p
        WHERE pv.gender = :gender
        AND p.category.id = :categoryId
    """)
    Page<ProductVariant> findByGenderAndCategory(
            @Param("gender") Gender gender,
            @Param("categoryId") Long categoryId,
            Pageable pageable
    );

    @Query("""
        SELECT pv
        FROM ProductVariant pv
        JOIN pv.product p
        WHERE pv.gender = :gender
        AND p.productCategory.id = :productCategoryId
    """)
    Page<ProductVariant> findByGenderAndProductCategory(
            @Param("gender") Gender gender,
            @Param("productCategoryId") Long categoryId,
            Pageable pageable
    );


    @Query("SELECT b.id as brandId, b.name as brandName, COUNT(pv.id) as variantCount " +
            "FROM ProductVariant pv JOIN pv.product p JOIN p.brand b " +
            "WHERE pv.gender = :gender " +
            "GROUP BY b.id, b.name")
    List<Object[]> countVariantsByBrandForGender(@Param("gender") Gender gender);


    @Query("""
        SELECT b.id as brandId, b.name as brandName, COUNT(pv.id) as variantCount
        FROM ProductVariant pv
        JOIN pv.product p
        JOIN p.brand b
        WHERE pv.gender = :gender
        AND p.category.id = :categoryId
        GROUP By b.id, b.name
    """)
    List<Object[]> countVariantsByBrandForGenderAndCategory(
            @Param("gender") Gender gender,
            @Param("categoryId") Long categoryId
    );

    @Query("""
        SELECT b.id as brandId, b.name as brandName, COUNT(pv.id) as variantCount
        FROM ProductVariant pv
        JOIN pv.product p
        JOIN p.brand b
        WHERE pv.gender = :gender
        AND p.subCategory.id = :subCategoryId
        GROUP By b.id, b.name
    """)
    List<Object[]> countVariantsByBrandForGenderAndSubCategory(
            @Param("gender") Gender gender,
            @Param("subCategoryId") Long subCategoryId
    );

    @Query("""
        SELECT b.id as brandId, b.name as brandName, COUNT(pv.id) as variantCount
        FROM ProductVariant pv
        JOIN pv.product p
        JOIN p.brand b
        WHERE pv.gender = :gender
        AND p.productCategory.id = :productCategoryId
        GROUP By b.id, b.name
    """)
    List<Object[]> countVariantsByBrandForGenderAndProductCategory(
            @Param("gender") Gender gender,
            @Param("productCategoryId") Long productCategoryId
    );
}
