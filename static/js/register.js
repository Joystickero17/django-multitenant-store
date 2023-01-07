const registerapp = new Vue({
    el:"#register-app",
    delimiters:["[[","]]"],
    data(){
        return {
            categories: [],
            category_search:"",
            showIncomeReason: false,
            showRifReason: false,
            in_transition:false,
            success_register_url: '/login/?registered=success',
            name:"",
            register_errors:[],
            last_name:"",
            email:"",
            password:"",
            password_repeat:"",
            rif:'',
            user_type:"",
            company_name:"",
            company_employee_number:"",
            company_anual_income:0,
            company_main_category: null,
            company_phone_number:"",
            company_logo:"",
            company_category:"",
            tags:"",
            step: 1,
            max_step:5,
            email_send_consent: false,
            errors:{}
        }
    },
    methods:{
        checkPassword(){
            console.log(this.password,this.password_repeat)
            not_equal = this.password != this.password_repeat
            empty = !this.password.length && !this.password_repeat.length
            if (not_equal){
                this.errors = {...this.errors, not_equal_password:"Las contraseñas no coinciden"}
            }
            if(this.password.length < 8){
                this.errors = {...this.errors, password:"La contraseña debe tener al menos 8 caracteres"}
            }
            if (empty){
                this.errors = {...this.errors, password:"Las contraseñas no pueden estar vacías"}
            }
        },
        sendData(){
            if (!this.checkForm()){
                return 
            }
            data = {
                name: this.name,
                last_name: this.last_name,
                email: this.email,
                password: this.password,
                password_repeat: this.password_repeat,
                user_type: this.user_type,
                email_send_consent: this.email_send_consent
            }
            console.log("data before",  console.log(JSON.stringify(data)))
            if (this.user_type == 'shop'){
                data = {
                    ...data, 
                    company_name: this.company_name,
                    company_anual_income: this.company_anual_income,
                    company_main_category: this.company_main_category,
                    company_employee_number: this.company_employee_number,
                    // company_phone_number: this.company_phone_number,
                }
            }else if(this.user_type == 'freelance'){
                

            }else{
                // data = {
                //     ...data,
                // }
            }
            console.log(JSON.stringify(data))
            axios.post("/api/register/", data, {withCredentials:true})
            .then((res)=>{
                if (res.status == 201){
                    window.location.href = this.success_register_url
                }
            })
            .catch((err)=>{
                console.log(err.response)
                let unflatten_errors = [
                    err.response.data.non_field_errors,
                    err.response.data.email,
                    err.response.data.name,
                    err.response.data.last_name,
                ]
                this.register_errors = unflatten_errors.map((item)=>{
                    if (item){
                        return item[0]
                    }
                })

                const myModal = new bootstrap.Modal(document.getElementById('registerModal'))
                myModal.show()
            })
        },
        isFinalStep(){
            user_final_step = this.step == 2 && this.user_type == 'customer'
            shop_final_step = this.step == 4 && this.user_type == 'shop'
            freelance_final_step = this.step == 3 && this.user_type == 'freelance'
            return user_final_step || shop_final_step || freelance_final_step
        },
        searchCategory(){
            axios.get("/api/category/", {params:{parents_only:true,search:this.category_search}})
            .then(res=>res.data.results)
            .then(data=>this.categories=data)
        },
        decreaseStep(){
            
            if (this.step<=1){
                this.step=1
                return
            }
            this.step--
        },
        increaseStep(){
            if (!this.checkForm()){
                return
            }
            if(this.isFinalStep()){
                return this.sendData()
            }
            if (this.step>=this.max_step){
                this.step=this.max_step
                return
            }
            this.step++
        },
        checkCompanyData(){
            if (this.user_type !== "shop"){
                return
            }
            if (this.step == 2){
                if (!this.company_name){
                    this.errors = {...this.errors, company_name:"Este campo es requerido"}
                }
                if (!this.company_employee_number){
                    this.errors = {...this.errors, company_employee_number:"este campo es requerido"}
                }
            }
            if (this.step == 3){
                if (!this.company_main_category){
                    this.errors = {...this.errors, company_main_category: "Seleccione una categoría"}
                }
            }
        },
        checkUserData(){
            let is_freelance_step = this.user_type == "freelance" && this.step == null
            let is_company_step = this.user_type == "shop" && this.step == 4

            if(this.user_type == "customer" && this.step == 2){
                if (!this.name){
                    this.errors = {...this.errors, user_type:"Debe seleccionar un tipo de cliente para continuar"}
                }
            }
        },
        checkForm(){
            this.errors = {}
            if (!this.user_type){
                this.errors = {...this.errors, user_type:"Debe seleccionar un tipo de cliente para continuar"}
            }
            this.checkCompanyData()
            this.checkUserData()
            if (this.isFinalStep()){
                this.checkPassword()
                if (!this.email_send_consent){
                    this.errors = {...this.errors, email_send_consent:"Debe dar consentimiento para enviar notificaciones y recibos a su correo electronico"}
                }
                if (!this.name){
                    this.errors = {...this.errors, name:"este campo es requerido"}
                }
                if (!this.last_name){
                    this.errors = {...this.errors, last_name:"este campo es requerido"}
                }
                if (!this.email){
                    this.errors = {...this.errors, email:"este campo es requerido"}
                }
            }
            
            console.log("errores ",JSON.stringify(this.errors))
            return Object.keys(this.errors).length == 0;
        },
        
    },
    mounted(){
        this.searchCategory()
    }
})
