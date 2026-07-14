package busness.ecommerce.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Data
@Builder
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Setting {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nameApp;

    @Column(nullable = false)
    private String nameDev;

    @Column(nullable = false)
    private String version;

    @Column(nullable = false)
    private String theme;

    @Column(nullable = false)
    private String textColor;

    @Column(nullable = false)
    private String currency;

    @Column(nullable = false)
    private String address;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String phone;

    @Column(nullable = false)
    private String logo;

    @Column(nullable = false)
    private Integer width;

    @Column(nullable = false)
    private Integer height;
}
