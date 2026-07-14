package busness.ecommerce.entity;

import busness.ecommerce.enums.Gender;
import busness.ecommerce.enums.ProductSource;
import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // ===== Informations générales =====
    @Column(nullable = false)
    private String name;

    @Column(length = 2000)
    private String description;

    // ===== Prix =====
    @Column(nullable = false)
    private Double price;

    // ===== Relation =====
    // Ajout conseillé

    @ManyToOne
    @JoinColumn(name = "category_id")
    private Category category;

    @ManyToOne
    @JoinColumn(name = "sub_category_id")
    private SubCategory subCategory;

    @ManyToOne
    @JoinColumn(name = "product_category_id")
    private ProductCategory productCategory;

    @ManyToOne
    @JoinColumn(name = "brand_id")
    private Brand brand;

    // NOUVEAU
    @ManyToOne
    @JoinColumn(name = "owner_id")
    private User owner;

    // TYPE DE PRODUIT
    @Enumerated(EnumType.STRING)
    private ProductSource source;

    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ProductImage> images = new ArrayList<>();
}
