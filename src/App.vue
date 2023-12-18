<template>
    <banerPage/>
    <router-view/>
    <footerPage/>
</template>
<script>
    import banerPage from "../src/components/banerPage.vue"
    import footerPage from "../src/components/footerPage.vue"
    export default
    {
        components:
        {
            banerPage,
            footerPage
        }
    }
</script>
<style lang="scss">
@import './style/style.scss';
#app 
{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: $font-color;
}
body
{
    margin: 0;
}
</style>
