package eajc.group.apv.mapper;

import eajc.group.apv.dto.BeneficiaryRequestDto;
import eajc.group.apv.dto.BeneficiaryResponseDto;
import eajc.group.apv.entity.Beneficiary;
import org.springframework.stereotype.Component;

@Component
public class BeneficiaryMapper {

    public Beneficiary toEntity(BeneficiaryRequestDto dto){
        Beneficiary beneficiary = new Beneficiary();

        beneficiary.setName(dto.getName());
        beneficiary.setCountry(dto.getCountry());
        beneficiary.setCity(dto.getCity());
        beneficiary.setBorough(dto.getBorough());
        beneficiary.setAddress(dto.getAddress());
        beneficiary.setPhone(dto.getPhone());
        beneficiary.setEmail(dto.getEmail());
        beneficiary.setDateExistence(dto.getDateExistence());
        beneficiary.setType(dto.getType());

        return beneficiary;
    }

    public BeneficiaryResponseDto toDto(Beneficiary beneficiary){

        BeneficiaryResponseDto dto = new BeneficiaryResponseDto();

        dto.setId(beneficiary.getId());
        dto.setPublicId(beneficiary.getPublicId());
        dto.setName(beneficiary.getName());
        dto.setCountry(beneficiary.getCountry());
        dto.setCity(beneficiary.getCity());
        dto.setBorough(beneficiary.getBorough());
        dto.setAddress(beneficiary.getAddress());
        dto.setPhone(beneficiary.getPhone());
        dto.setEmail(beneficiary.getEmail());
        dto.setDateExistence(beneficiary.getDateExistence());
        dto.setType(beneficiary.getType().name());

        return  dto;
    }
}
